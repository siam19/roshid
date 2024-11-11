import Image from 'next/image'

type ImageBlockContent = {
  url: string
  title: string
  style: {
    type: string
    alignment: string
  }
}

export function ImageBlock({ content }: { content: ImageBlockContent }) {
  const { url, title, style } = content

  const aspectRatio = style.type === '4x3' ? 'aspect-[4/3]' : 'aspect-square'
  const alignment = style.alignment === 'horizontal' ? 'w-full' : 'w-1/2 mx-auto'

  return (
    <div className={`${alignment} ${aspectRatio} relative mb-4`}>
      <Image
        src={url}
        alt={title}
        fill
        className="object-cover rounded-lg"
      />
    </div>
  )
}