interface PageContainerProps {
  children: React.ReactNode;
  title?: string;
  description?: string;
}

/**
 * Wrapper component for page content with consistent styling.
 */
export function PageContainer({
  children,
  title,
  description,
}: PageContainerProps) {
  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      {title && (
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-slate-100">{title}</h1>
          {description && (
            <p className="mt-2 text-slate-400">{description}</p>
          )}
        </div>
      )}
      {children}
    </div>
  );
}
