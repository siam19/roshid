import { ImageBlock } from './blocks/ImageBlock'
import { TextBlock } from './blocks/TextBlock'
import { ProductCollectionBlock } from './blocks/ProductCollectionBlock'

type Block = {
  index: number
  type: string
  content: any
}

export function BlockRenderer({ block, userId }: { block: Block; userId: string }) {
  switch (block.type) {
    case 'img':
      return <ImageBlock content={block.content} />
    case 'text':
      return <TextBlock content={block.content} />
    case 'productCollection':
      return <ProductCollectionBlock content={block.content} userId={userId} />
    default:
      console.warn(`Unknown block type: ${block.type}`)
      return null
  }
}