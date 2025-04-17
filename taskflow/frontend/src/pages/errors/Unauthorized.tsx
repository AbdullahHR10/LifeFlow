import type React from "react"

import Button from "../../components/Button"
import { LuLock } from "react-icons/lu"
import { FaArrowLeft } from "react-icons/fa"
import { useNavigate } from "react-router-dom"

const Unauthorized: React.FC = () => {
  const navigate = useNavigate()
  const handleClick = () => {
    navigate("/")
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-[70vh] px-4 text-center">
      <div className="rounded-full bg-muted p-6 mb-6 bg-gray-200">
        <LuLock className="h-12 w-12 text-muted-foreground" aria-hidden="true" />
      </div>
      <h1 className="text-4xl font-bold tracking-tight mb-2">Unauthorized Access</h1>
      <p className="text-muted-foreground text-lg mb-8 max-w-md">
        Sorry, you don't have permission to access this page. Please log in or contact an administrator for assistance.
      </p>
      <Button text="Back to home" color="dark" icon={<FaArrowLeft className="h-3 w-3" />} onClick={handleClick} />
    </div>
  )
}

export default Unauthorized
