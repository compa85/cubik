import * as React from "react";
import { Slot } from "@radix-ui/react-slot";
import { cva } from "class-variance-authority";
import { cn } from "@/lib/utils";

const buttonVariants = cva("inline-flex items-center justify-center whitespace-nowrap font-medium tracking-wide transition-colors", {
  variants: {
    variant: {
      solid: "shadow-sm",
      outline: "border-2 shadow-sm",
    },
    size: {
      sm: "h-8 gap-x-1 rounded-lg px-3 text-xs",
      md: "h-10 gap-x-2 rounded-xl px-3 text-sm",
      lg: "h-12 gap-x-2 rounded-xl px-6",
    },
    color: {
      primary: "text-primary-foreground",
      secondary: "text-secondary-foreground",
    },
  },
  compoundVariants: [
    // =============== SOLID ===============
    {
      variant: "solid",
      color: "primary",
      class: "bg-primary hover:bg-primary/90",
    },
    {
      variant: "solid",
      color: "secondary",
      class: "bg-secondary hover:bg-secondary/90",
    },
    // ============== OUTLINE ==============
    {
      variant: "outline",
      color: "primary",
      class: "border-primary text-primary hover:border-primary/90 hover:text-primary/90",
    },
    {
      variant: "outline",
      color: "secondary",
      class: "border-secondary text-secondary hover:border-secondary/90 hover:text-secondary/90",
    },
    // =============== GHOST ===============
    {
      variant: "ghost",
      color: "primary",
      class: "text-primary hover:bg-primary/70 hover:text-primary-foreground",
    },
    {
      variant: "ghost",
      color: "secondary",
      class: "text-secondary-foreground hover:bg-secondary/70",
    },
    // ============== DISABLED ==============
    {
      isDisabled: true,
      class: "pointer-events-none opacity-50",
    },
    // ============= ICON ONLY =============
    {
      isIconOnly: true,
      size: "sm",
      class: "size-8 px-2",
    },
    {
      isIconOnly: true,
      size: "md",
      class: "size-10 px-2",
    },
    {
      isIconOnly: true,
      size: "lg",
      class: "size-12 px-2",
    },
  ],
  defaultVariants: {
    variant: "solid",
    size: "md",
    color: "primary",
  },
});

const Button = React.forwardRef(
  ({ className, variant, size, color, isDisabled = false, isIconOnly = false, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : "button";
    return <Comp className={cn(buttonVariants({ variant, size, color, isDisabled, isIconOnly, className }))} ref={ref} {...props} />;
  },
);
Button.displayName = "Button";

export { Button, buttonVariants };
