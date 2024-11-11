import { cn } from "@/lib/utils"

type TextBlockContent = {
  text: string
  style: {
    type: 'header' | 'paragraph'
    alignment: 'left' | 'center' | 'right'
  }
}

export function TextBlock({ content }: { content: TextBlockContent }) {
  const { text, style } = content

  const textClass = cn(
    "mb-4",
    {
      "text-2xl font-bold": style.type === "header",
      "text-base": style.type === "paragraph",
      "text-left": style.alignment === "left",
      "text-center": style.alignment === "center",
      "text-right": style.alignment === "right",
    }
  )

  return (
    <div className={textClass}>
      {text}
    </div>
  )
}