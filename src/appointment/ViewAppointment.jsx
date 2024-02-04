import React from 'react'
import { useState, useEffect } from "react";
import {
  FormControl,
  FormLabel,
  Input,
  Button,
  Box,
  Select,
  Heading,
  useToast,
} from "@chakra-ui/react";
import { useNavigate } from "react-router-dom";
export default function ViewAppointment() {
  const [licenseNumber, setLicenseNumber] = useState("");
  const [dateOfBirth, setDateOfBirth] = useState("");
  const [email, setEmail] = useState("");
  const [appointmentID, setaAppointmentID] = useState("");
  const navigate = useNavigate();
  const toast = useToast();
  const handleSubmit = async (event) => {
    event.preventDefault();
    if(licenseNumber == "" || licenseNumber == undefined || licenseNumber == null){
      alert("Please provide license number.")
    }
    else if(dateOfBirth == "" || dateOfBirth == undefined || dateOfBirth == null){
      alert("Please provide date of birth.")
    }
    else if(appointmentID == "" || appointmentID == undefined || appointmentID == null){
      alert("Please provide appointment id.")
    }
   
    else{
      
      let URL = import.meta.env.VITE_API_GATEWAY_URL;
      let STEP_FUNCTION_ARN = import.meta.env.VITE_STEP_FUNCTION_ARN;
      
      let input_data = JSON.stringify({
          "type": "VIEW",
          "license_number" : licenseNumber,
          "date_of_birth": dateOfBirth,
          "appointment_id": appointmentID
      })  
      const data = {
        input: input_data,
        stateMachineArn: STEP_FUNCTION_ARN
      };
      const response = await fetch(URL , {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      const body = await response.json()

      if(body.status){
        toast({
          title: body.message,
          status: "success",
          isClosable: true,
        });
        navigate("/appointment-details/",{"state": {"data" : body.data}});
      }
      else{
        alert(body.message)
      }
      
    }
  };

  const handleCancel = (event) => {
    navigate("/");
  };

  useEffect(() => {
    var today = new Date().toISOString().split('T')[0];
    document.getElementById("dateOfBirth").setAttribute("max", today);
}, [])

  return (
    <Box maxWidth="500px" mx="auto">
      <Heading as="h1" textAlign="center" mb="8" textColor={"teal"} pt="10">
        View an Appointment
      </Heading>
      <form onSubmit={handleSubmit}>
        <FormControl id="licenseNumber" mb="4">
          <FormLabel>License Number</FormLabel>
          <Input
            type="text"
            placeholder="Enter your license number"
            value={licenseNumber}
            onChange={(event) => setLicenseNumber(event.target.value)}
          />
        </FormControl>
        
        <FormControl id="dateOfBirth" mb="4">
          <FormLabel>Date of Birth</FormLabel>
          <Input
            type="date"
            placeholder="Enter your date of birth"
            value={dateOfBirth}
            onChange={(event) => setDateOfBirth(event.target.value)}
          />
        </FormControl>
        <FormControl id="appointment" mb="4">
          <FormLabel>Appointment ID</FormLabel>
          <Input
            type="text"
            placeholder="Enter your payment appointment id."
            value={appointmentID}
            onChange={(event) => setaAppointmentID(event.target.value)}
          />
        </FormControl>
        <FormControl id="email" mb="4">
          <FormLabel>Email address</FormLabel>
          <Input
            type="email"
            placeholder="Enter your email address"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
          />
        </FormControl>
  
        <Button
          variant="outline"
          colorScheme="teal"
          onClick={handleSubmit}
          mr="10"
        >
          Submit
        </Button>
        <Button variant="outline" colorScheme="teal" onClick={handleCancel}>
          Cancel
        </Button>
      </form>
    </Box>
  )
}
