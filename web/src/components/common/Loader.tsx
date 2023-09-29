import { motion } from 'framer-motion';
const Loader = () => {
  return (
    // <div className="flex gap-2">
    //   <span className="h-4 w-4 rounded-full bg-info"></span>
    //   <span className="h-4 w-4 rounded-full bg-success"></span>
    //   <span className="h-4 w-4 rounded-full bg-warning"></span>
    //   <span className="h-4 w-4 rounded-full bg-error"></span>
    // </div>
    <div>
      <motion.div
        className="my-16 flex h-16 w-48 items-center justify-center rounded-lg bg-neutral text-center font-bold text-base-100"
        animate={{
          // jitter
          x: [-2, 3, -4, 2, -1, 0, -2, 3, -4, 2, -1, -2],
          y: [-3, 2, -1, 0, -2, 3, -4, 2, -1, 0, -2, -3],
        }}
        transition={{ duration: 1.5, repeat: Infinity }}
      >
        Joining Room
        <motion.div
          className="absolute -left-1/4 flex animate-pulse flex-col gap-2"
          animate={{
            y: ['-20%', '20%', '-20%'],
          }}
          transition={{ duration: 1.2, repeat: Infinity, ease: [0.17, 0.67, 0.83, 0.67] }}
        >
          <motion.line
            className="block h-1 w-16 rounded-full bg-neutral"
            animate={{
              x: ['0%', '50%', '0%'],
            }}
            transition={{ duration: 1.2, repeat: Infinity, ease: [0.17, 0.67, 0.83, 0.67] }}
          />
          <motion.line
            className="block h-1 w-16 rounded-full bg-neutral"
            animate={{
              x: ['0%', '50%', '0%'],
            }}
            transition={{ duration: 0.8, repeat: Infinity, ease: [0.17, 0.67, 0.83, 0.67] }}
          />
          <motion.line
            className="block h-1 w-16 rounded-full bg-neutral"
            animate={{
              x: ['0%', '50%', '0%'],
            }}
            transition={{ duration: 1.1, repeat: Infinity, ease: [0.17, 0.67, 0.83, 0.67] }}
          />
        </motion.div>
      </motion.div>
    </div>
  );
};

export { Loader };
