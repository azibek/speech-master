import { motion } from "framer-motion";
import clsx from "classnames";

type Props = {
  id: string;
  label: string;
  active: boolean;
  onClick: () => void;
};

/**
 * PersonaCard
 * -------------------------------------
 * • Displays the persona’s name (and image later if you like).
 * • Highlights when selected.
 * • Scales up slightly on hover.
 */
export default function PersonaCard({ label, active, onClick }: Props) {
  return (
    <motion.button
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.98 }}
      onClick={onClick}
      className={clsx(
        "w-40 h-40 rounded-2xl p-4 shadow-md flex items-center justify-center text-center transition",
        active
          ? "ring-4 ring-primary text-primary font-semibold shadow-lg"
          : "bg-white hover:shadow-lg"
      )}
    >
      {label}
    </motion.button>
  );
}
