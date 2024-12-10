import { notFound } from 'next/navigation'
import { BlockRenderer } from '../../blocks/BlockRenderer'
import { Skeleton } from "@/components/ui/skeleton"

// This ensures the page is dynamically rendered for each request
export const dynamic = 'force-dynamic'

async function getUserPage(userId: string) {
  let res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}pages/${userId}`)
  return res.json()
}

export default async function UserPage({ params }: { params: Promise<{ userId: string }> }) {
  try {
    const { userId } = await params
    const userPageData = await getUserPage(userId)

    if (!userPageData) {
      notFound()
    }

    return (
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold mb-6">{userPageData.title}</h1>
        {userPageData.blocks.map((block) => (
          <BlockRenderer key={block.index} block={block} userId={userId} />
        ))}
      </div>
    )
  } catch (error) {
    console.error('Failed to fetch user page:', error)
    return <div className="container mx-auto px-4 py-8 text-center text-red-500">Failed to load page. Please try again later.</div>
  }
}

function LoadingSkeleton() {
  return (
    <div className="container mx-auto px-4 py-8">
      <Skeleton className="h-10 w-3/4 mb-6" />
      <Skeleton className="h-40 w-full mb-4" />
      <Skeleton className="h-20 w-full mb-4" />
      <Skeleton className="h-60 w-full mb-4" />
    </div>
  )
}