# Create React Component

Create a React component in apps/ui/src/components/

## Requirements

- Component name: {ComponentName}
- Location: {folder path}
- Props: {list props}
- Client/Server: {client or server component}

## Template (Server Component - Default)
```typescript
import { cn } from "@/lib/utils";

interface {ComponentName}Props {
  className?: string;
  // Add props here
}

export function {ComponentName}({ className }: {ComponentName}Props) {
  return (
    <div className={cn("", className)}>
      {/* Component content */}
    </div>
  );
}
```

## Template (Client Component)
```typescript
"use client";

import { useState } from "react";
import { cn } from "@/lib/utils";

interface {ComponentName}Props {
  className?: string;
  // Add props here
}

export function {ComponentName}({ className }: {ComponentName}Props) {
  const [state, setState] = useState();

  return (
    <div className={cn("", className)}>
      {/* Component content */}
    </div>
  );
}
```

## Watch Out For
- Use "use client" only when needed (useState, useEffect, event handlers)
- Always type props with an interface
- Use cn() for className merging (from shadcn/ui)
- Keep components small and focused
- Export from components/index.ts if it's a shared component
