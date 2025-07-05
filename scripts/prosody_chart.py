#!/usr/bin/env python
"""
Clean audio using ML-based noise removal and generate prosody visualization.

This script uses:
1. Facebook's Demucs for audio source separation/noise removal
2. Alternatively, Meta's Denoiser for speech enhancement
3. Then generates prosody analysis

Usage:
    python ml_prosody_viz.py input.wav output_dir/ [--model demucs|denoiser|noisereduce]
"""

import sys
import pathlib
import tempfile
import subprocess
import numpy as np
import matplotlib.pyplot as plt
import parselmouth
import parselmouth.praat as praat
import librosa
import soundfile as sf

try:
    import torch
    import torchaudio
    from demucs.pretrained import get_model
    from demucs.apply import apply_model
    DEMUCS_AVAILABLE = True
except ImportError:
    DEMUCS_AVAILABLE = False

try:
    import noisereduce as nr
    NOISEREDUCE_AVAILABLE = True
except ImportError:
    NOISEREDUCE_AVAILABLE = False

# ─── ML Audio Cleaning ────────────────────────────────────────────────────
def clean_audio_demucs(audio_path, output_path, model_name="dns64"):
    """Clean audio using Facebook's Demucs model."""
    if not DEMUCS_AVAILABLE:
        print("Error: Demucs not installed. Run: pip install demucs")
        return False
    
    print(f"Loading Demucs model: {model_name}")
    try:
        # Load pre-trained model
        model = get_model(model_name)
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model.to(device)
        
        # Load audio
        print(f"Loading audio: {audio_path}")
        waveform, sample_rate = torchaudio.load(str(audio_path))
        waveform = waveform.to(device)
        
        # Apply model
        print("Applying Demucs denoising...")
        with torch.no_grad():
            enhanced = apply_model(model, waveform[None], device=device)[0]
        
        # Save enhanced audio
        enhanced_cpu = enhanced.cpu()
        torchaudio.save(str(output_path), enhanced_cpu, sample_rate)
        
        print(f"✅ Audio cleaned with Demucs: {output_path}")
        return True
        
    except Exception as e:
        print(f"Error with Demucs: {e}")
        return False

def clean_audio_noisereduce(audio_path, output_path):
    """Clean audio using noisereduce library."""
    if not NOISEREDUCE_AVAILABLE:
        print("Error: noisereduce not installed. Run: pip install noisereduce")
        return False
    
    try:
        print(f"Loading audio: {audio_path}")
        # Load audio
        audio, sr = librosa.load(str(audio_path), sr=None)
        
        print("Applying noise reduction...")
        # Apply noise reduction
        reduced_noise = nr.reduce_noise(y=audio, sr=sr, prop_decrease=0.8)
        
        # Save cleaned audio
        sf.write(str(output_path), reduced_noise, sr)
        
        print(f"✅ Audio cleaned with noisereduce: {output_path}")
        return True
        
    except Exception as e:
        print(f"Error with noisereduce: {e}")
        return False

def clean_audio_whisper_style(audio_path, output_path):
    """Clean audio using Whisper-style preprocessing."""
    try:
        print(f"Loading audio: {audio_path}")
        # Load audio like Whisper does
        audio, sr = librosa.load(str(audio_path), sr=16000)  # Whisper uses 16kHz
        
        print("Applying Whisper-style preprocessing...")
        
        # Apply similar preprocessing to what Whisper uses internally
        # 1. Normalize
        audio = audio / np.max(np.abs(audio))
        
        # 2. Apply mild high-pass filter to remove low-frequency noise
        from scipy.signal import butter, filtfilt
        b, a = butter(4, 80, btype='high', fs=sr)
        audio = filtfilt(b, a, audio)
        
        # 3. Apply spectral gating (similar to what Whisper does)
        # Compute short-time energy
        hop_length = 512
        frame_length = 2048
        energy = librosa.feature.rms(y=audio, frame_length=frame_length, hop_length=hop_length)[0]
        
        # Apply energy-based gating
        energy_threshold = np.percentile(energy, 20)  # Bottom 20% is likely noise
        times = librosa.frames_to_time(np.arange(len(energy)), sr=sr, hop_length=hop_length)
        
        # Smooth the gate
        gate = energy > energy_threshold
        gate_smooth = np.convolve(gate.astype(float), np.ones(5)/5, mode='same')
        
        # Apply gate to audio
        audio_gated = []
        for i, t in enumerate(times):
            start_sample = int(t * sr)
            end_sample = int((t + hop_length/sr) * sr)
            if end_sample > len(audio):
                end_sample = len(audio)
            
            gate_factor = 0.1 + 0.9 * gate_smooth[i]  # Never fully gate, just attenuate
            audio_gated.extend(audio[start_sample:end_sample] * gate_factor)
        
        audio_gated = np.array(audio_gated[:len(audio)])
        
        # 4. Final normalization
        audio_gated = audio_gated / (np.max(np.abs(audio_gated)) + 1e-8)
        
        # Save processed audio
        sf.write(str(output_path), audio_gated, sr)
        
        print(f"✅ Audio cleaned with Whisper-style preprocessing: {output_path}")
        return True
        
    except Exception as e:
        print(f"Error with Whisper-style preprocessing: {e}")
        return False

# ─── Voice Quality Metrics ────────────────────────────────────────────────
def voice_metrics(sound, pp):
    """Return key voice-quality numbers as dict."""
    try:
        jitter = praat.call(pp, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3)
        shimmer = praat.call([sound, pp], "Get shimmer (local)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
        hnr = sound.to_harmonicity().values.mean()
        
        # CPP calculation with error handling
        try:
            power_cepstrum = praat.call(sound, "To PowerCepstrum", 75, 0.002)
            cpp = praat.call(power_cepstrum, "Get peak prominence", 60, 333.3, "Parabolic", 0.001, 0.05, "Straight", "Robust")
        except:
            try:
                spectrum = sound.to_spectrum()
                power_cepstrum = praat.call(spectrum, "To PowerCepstrum")
                cpp = praat.call(power_cepstrum, "Get peak prominence", 60, 333.3, "Parabolic", 0.001, 0.05, "Straight", "Robust")
            except:
                cpp = np.nan
        
        return dict(jitter_pct=jitter * 100,
                    shimmer_pct=shimmer * 100,
                    HNR_dB=hnr,
                    CPP_dB=cpp)
    except Exception as e:
        print(f"Warning: Error calculating voice metrics: {e}")
        return dict(jitter_pct=np.nan, shimmer_pct=np.nan, HNR_dB=np.nan, CPP_dB=np.nan)

# ─── Prosody Visualization ────────────────────────────────────────────────
def generate_prosody_chart(audio_path: pathlib.Path, out_dir: pathlib.Path, title_suffix=""):
    """Generate prosody visualization from audio file."""
    try:
        snd = parselmouth.Sound(str(audio_path))
        dur = snd.get_total_duration()
        
        print(f"Analyzing audio: {dur:.2f} seconds")
        
        # Extract prosodic features
        pitch = snd.to_pitch(time_step=0.01, pitch_floor=75, pitch_ceiling=500)
        intensity_obj = snd.to_intensity(time_step=0.01)
        specgram = snd.to_spectrogram(window_length=0.03, maximum_frequency=8000)
        
        # Get voice quality metrics
        try:
            pp = praat.call(snd, "To PointProcess (periodic, cc)", 75, 500)
            metrics = voice_metrics(snd, pp)
        except:
            print("Warning: Could not calculate voice metrics")
            metrics = dict(jitter_pct=np.nan, shimmer_pct=np.nan, HNR_dB=np.nan, CPP_dB=np.nan)
        
        # Create visualization
        fig, ax = plt.subplots(figsize=(13, 8), constrained_layout=True)
        
        # 1. Spectrogram background
        ax.imshow(specgram.values.T,
                  extent=[0, dur, 0, specgram.ymax],
                  origin="lower",
                  aspect="auto",
                  cmap="Greys",
                  alpha=0.6)
        
        # 2. Pitch contour
        f0_values = pitch.selected_array['frequency']
        t_pitch = pitch.xs()
        
        if len(t_pitch) != len(f0_values):
            t_pitch = np.arange(len(f0_values)) * 0.01
        
        voiced_mask = f0_values > 0
        if np.any(voiced_mask):
            ax.plot(t_pitch[voiced_mask], f0_values[voiced_mask], 'b-', 
                   label="Pitch (Hz)", linewidth=2)
        
        # 3. Intensity
        intensity_values = intensity_obj.values[0]
        t_intensity = intensity_obj.xs()
        
        if len(t_intensity) != len(intensity_values):
            t_intensity = np.arange(len(intensity_values)) * 0.01
        
        ax2 = ax.twinx()
        ax2.plot(t_intensity, intensity_values, color="tab:orange", 
                label="Intensity (dB)", linewidth=2, alpha=0.8)
        ax2.set_ylabel("Intensity (dB)")
        
        # Styling
        ax.set_title(f"Prosodic Analysis{title_suffix}: {audio_path.name}", fontsize=15)
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Frequency (Hz)")
        ax.set_ylim(0, 8000)
        ax.set_xlim(0, dur)
        ax.grid(alpha=0.2)
        
        # Legend
        lines, labels = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax2.legend(lines + lines2, labels + labels2, loc="upper right")
        
        # Voice metrics box
        cpp_text = f"{metrics['CPP_dB']:.2f} dB" if not np.isnan(metrics['CPP_dB']) else "N/A"
        hnr_text = f"{metrics['HNR_dB']:.1f} dB" if not np.isnan(metrics['HNR_dB']) else "N/A"
        jitter_text = f"{metrics['jitter_pct']:.2f}%" if not np.isnan(metrics['jitter_pct']) else "N/A"
        shimmer_text = f"{metrics['shimmer_pct']:.2f}%" if not np.isnan(metrics['shimmer_pct']) else "N/A"
        
        text = (f"Jitter:  {jitter_text}\n"
                f"Shimmer: {shimmer_text}\n"
                f"HNR:     {hnr_text}\n"
                f"CPP:     {cpp_text}")
        fig.text(0.80, 0.25, text,
                 bbox=dict(boxstyle="round,pad=0.5", facecolor="white", alpha=0.7),
                 fontsize=10, ha="left", va="center")
        
        # Save
        suffix = "_cleaned" if title_suffix else ""
        out_path = out_dir / (audio_path.stem + f"_prosody{suffix}.png")
        fig.savefig(out_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Prosody chart saved: {out_path}")
        return True
        
    except Exception as e:
        print(f"Error generating prosody chart: {e}")
        return False

# ─── Main Function ────────────────────────────────────────────────────────
def main():
    if len(sys.argv) < 3:
        print("Usage: python ml_prosody_viz.py input.wav output_dir/ [--model demucs|denoiser|noisereduce|whisper]")
        sys.exit(1)
    
    audio_path = pathlib.Path(sys.argv[1])
    out_dir = pathlib.Path(sys.argv[2])
    
    # Parse model argument
    model_choice = "noisereduce"  # default
    if len(sys.argv) > 3 and sys.argv[3] == "--model":
        if len(sys.argv) > 4:
            model_choice = sys.argv[4]
    
    if not audio_path.exists():
        print(f"Error: Audio file {audio_path} not found")
        sys.exit(1)
    
    out_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"🎵 Processing: {audio_path}")
    print(f"📊 Output directory: {out_dir}")
    print(f"🤖 Using model: {model_choice}")
    
    # Generate prosody chart for original audio
    print("\n=== Analyzing Original Audio ===")
    generate_prosody_chart(audio_path, out_dir, title_suffix="")
    
    # Clean audio using selected ML model
    print(f"\n=== Cleaning Audio with {model_choice} ===")
    cleaned_path = out_dir / (audio_path.stem + "_cleaned.wav")
    
    if model_choice == "demucs":
        success = clean_audio_demucs(audio_path, cleaned_path)
    elif model_choice == "noisereduce":
        success = clean_audio_noisereduce(audio_path, cleaned_path)
    elif model_choice == "whisper":
        success = clean_audio_whisper_style(audio_path, cleaned_path)
    else:
        print(f"Unknown model: {model_choice}")
        print("Available models: demucs, noisereduce, whisper")
        sys.exit(1)
    
    if success:
        # Generate prosody chart for cleaned audio
        print("\n=== Analyzing Cleaned Audio ===")
        generate_prosody_chart(cleaned_path, out_dir, title_suffix=" (Cleaned)")
        
        print(f"\n✅ Complete! Check {out_dir} for:")
        print(f"   - Original prosody chart: {audio_path.stem}_prosody.png")
        print(f"   - Cleaned audio: {cleaned_path.name}")
        print(f"   - Cleaned prosody chart: {audio_path.stem}_prosody_cleaned.png")
    else:
        print("❌ Audio cleaning failed")

if __name__ == "__main__":
    main()