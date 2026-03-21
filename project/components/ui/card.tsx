import * as React from "react";
import { cn } from "@/lib/utils";
import { motion, HTMLMotionProps } from "framer-motion";

type CardProps = Omit<HTMLMotionProps<"div">, "ref"> & {
  className?: string;
};

const cardVariants = {
  initial: { 
    opacity: 0, 
    y: 20 
  },
  animate: { 
    opacity: 1, 
    y: 0,
    transition: {
      duration: 0.5,
      ease: "easeOut"
    }
  },
  hover: {
    scale: 1.02,
    boxShadow: "0 20px 25px -5px rgba(134, 89, 255, 0.1), 0 8px 10px -6px rgba(134, 89, 255, 0.1)",
    borderColor: "rgba(134, 89, 255, 0.3)",
    transition: {
      duration: 0.3,
      ease: "easeInOut"
    }
  }
};

const contentVariants = {
  initial: { 
    opacity: 0, 
    y: 10 
  },
  animate: {
    opacity: 1,
    y: 0,
    transition: {
      duration: 0.3,
      delay: 0.2
    }
  }
};

const Card = React.forwardRef<HTMLDivElement, CardProps>(
  ({ className, ...props }, ref) => (
    <motion.div
      ref={ref}
      variants={cardVariants}
      initial="initial"
      animate="animate"
      whileHover="hover"
      className={cn(
        "rounded-xl border border-[#8659ff]/20",
        "bg-[#2d1159]/50 backdrop-blur-sm",
        "shadow-lg shadow-[#8659ff]/10",
        "transition-all duration-300",
        className
      )}
      {...props}
    />
  )
);
Card.displayName = "Card";

type CardHeaderProps = Omit<HTMLMotionProps<"div">, "ref">;

const CardHeader = React.forwardRef<HTMLDivElement, CardHeaderProps>(
  ({ className, ...props }, ref) => (
    <motion.div
      ref={ref}
      variants={contentVariants}
      initial="initial"
      animate="animate"
      className={cn(
        "flex flex-col space-y-1.5 p-6",
        "border-b border-[#8659ff]/20",
        className
      )}
      {...props}
    />
  )
);
CardHeader.displayName = "CardHeader";

type CardTitleProps = Omit<HTMLMotionProps<"h3">, "ref">;

const CardTitle = React.forwardRef<HTMLHeadingElement, CardTitleProps>(
  ({ className, ...props }, ref) => (
    <motion.h3
      ref={ref}
      whileHover={{ scale: 1.01 }}
      className={cn(
        "font-bold leading-tight tracking-tight text-lg",
        "bg-gradient-to-r from-[#a587ff] to-[#6c3aed] bg-clip-text text-transparent",
        className
      )}
      {...props}
    />
  )
);
CardTitle.displayName = "CardTitle";

type CardDescriptionProps = Omit<HTMLMotionProps<"p">, "ref">;

const CardDescription = React.forwardRef<HTMLParagraphElement, CardDescriptionProps>(
  ({ className, ...props }, ref) => (
    <motion.p
      ref={ref}
      variants={contentVariants}
      initial="initial"
      animate="animate"
      className={cn(
        "text-sm text-[#c4b1ff]",
        className
      )}
      {...props}
    />
  )
);
CardDescription.displayName = "CardDescription";

type CardContentProps = Omit<HTMLMotionProps<"div">, "ref">;

const CardContent = React.forwardRef<HTMLDivElement, CardContentProps>(
  ({ className, ...props }, ref) => (
    <motion.div
      ref={ref}
      variants={contentVariants}
      initial="initial"
      animate="animate"
      className={cn(
        "p-6 pt-0",
        "relative",
        "after:absolute after:bottom-0 after:left-0 after:right-0 after:h-px",
        "after:bg-gradient-to-r after:from-transparent after:via-[#8659ff]/20 after:to-transparent",
        className
      )}
      {...props}
    />
  )
);
CardContent.displayName = "CardContent";

type CardFooterProps = Omit<HTMLMotionProps<"div">, "ref">;

const CardFooter = React.forwardRef<HTMLDivElement, CardFooterProps>(
  ({ className, ...props }, ref) => (
    <motion.div
      ref={ref}
      variants={contentVariants}
      initial="initial"
      animate="animate"
      className={cn(
        "flex items-center p-6 pt-4",
        "bg-gradient-to-t from-[#2d1159]/30 to-transparent",
        className
      )}
      {...props}
    />
  )
);
CardFooter.displayName = "CardFooter";

export { Card, CardHeader, CardFooter, CardTitle, CardDescription, CardContent };