import React, { useState } from 'react'
import { PlusCircle } from 'lucide-react'
import NewOrderModal from './modals/NewOrderModal'

const NewOrderButton = () => {
  const [isModalOpen, setIsModalOpen] = useState(false)

  const openModal = () => {
    setIsModalOpen(true)
  }

  const closeModal = () => {
    setIsModalOpen(false)
  }

  return (
    <div className="flex flex-col items-center my-12">
      <div
        onClick={openModal}
        className="cursor-pointer bg-blue-100 hover:bg-blue-200 transition-colors duration-300 rounded-lg p-6 text-center shadow-md"
      >
        <PlusCircle className="mx-auto mb-2" size={24} />
        <h2 className="text-xl font-medium mb-2">New Order</h2>
        <p className="text-sm text-gray-600">
          Create new Order or Press CTRL+V to create from Screenshot
        </p>
      </div>

      <NewOrderModal isOpen={isModalOpen} onClose={closeModal} />
    </div>
  )
}

export default NewOrderButton