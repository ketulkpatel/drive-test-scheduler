import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import Home from './Home'
import BookAppointment from './appointment/BookAppointment'
import CancelAppointment from './appointment/CancelAppointment'
import RescheduleAppointment from './appointment/RescheduleAppointment'
import ViewAppointment from './appointment/ViewAppointment'
import AppoinmentDetails from './appointment/AppoinmentDetails'
function App() {
  const router = createBrowserRouter([
    {
      path: "/",
      element: <Home/>
    },
    {
      path: "/book-appointment",
      element: <BookAppointment/>
    },
    {
      path: "/cancel-appointment",
      element: <CancelAppointment/>
    },
    {
      path: "/reschedule-appointment",
      element: <RescheduleAppointment/>
    },
    {
      path: "/view-appointment",
      element: <ViewAppointment/>
    },
    {
      path: "/appointment-details",
      element: <AppoinmentDetails/>
    }
  ])
  return (
   <RouterProvider router={router}></RouterProvider>
  )
}

export default App
