import React, { useEffect } from "react";
import { useState } from "react";
import {
  FormControl,
  FormLabel,
  Input,
  Button,
  Box,
  Select,
  Heading,
  useToast
} from "@chakra-ui/react";
import { useNavigate } from "react-router-dom";
import.meta.env.API_GATEWAY_URL

export default function BookAppointment() {
  
  const [licenseNumber, setLicenseNumber] = useState("");
  const [dateOfBirth, setDateOfBirth] = useState("");
  const [email, setEmail] = useState("");
  const [appointmentDate, setAppointmentDate] = useState("");
  const [appointmentTimeSlot, setAppointmentTimeSlot] = useState("");
  const [receiptID, setReceiptID] = useState("");
  const navigate = useNavigate();
  const toast = useToast();


  useEffect(() => {
    var today = new Date().toISOString().split('T')[0];
    var twoWeeksFromNow = new Date(new Date().getTime() + (14 * 24 * 60 * 60 * 1000)).toISOString().split('T')[0];
    document.getElementById("appointmentDate").setAttribute("min", today);
    document.getElementById("appointmentDate").setAttribute("max", twoWeeksFromNow);
    document.getElementById("dateOfBirth").setAttribute("max", today);
}, [])



  const handleSubmit = async (event) => {
    
    if(licenseNumber == "" || licenseNumber == undefined || licenseNumber == null){
      alert("Please provide license number.")
    }
    else if(dateOfBirth == "" || dateOfBirth == undefined || dateOfBirth == null){
      alert("Please provide date of birth.")
    }
    else if(receiptID == "" || receiptID == undefined || receiptID == null){
      alert("Please provide payment receipt id.")
    }
    else if(!/^([a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4})$/.test(
      email
    )){
      alert("Please provide valid email.")
    }
    else if(appointmentDate == "" || appointmentDate == undefined || appointmentDate == null){
      alert("Please provide appointment date.")
    }
    else if(appointmentTimeSlot == "" || appointmentTimeSlot == undefined || appointmentTimeSlot == null){
      alert("Please provide appointment slot.")
    }

    else{
      
      let URL = import.meta.env.VITE_API_GATEWAY_URL;
      let STEP_FUNCTION_ARN = import.meta.env.VITE_STEP_FUNCTION_ARN;

      let input_data = JSON.stringify({
        type: "BOOK",
        license_number : licenseNumber,
        date_of_birth: dateOfBirth,
        email_address: email,
        receipt_id: receiptID,
        appointment_date: appointmentDate,
        appointment_slot: appointmentTimeSlot
      })
      
      const data = {
        input: input_data,
        stateMachineArn: STEP_FUNCTION_ARN
      };

     
      const response = await fetch(URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data)
      });
      
      const body = await response.json();

      if(body.status){
        toast({
          title: body.message,
          status: "success",
          isClosable: true,
        });

        navigate("/");
      }
      else{
        alert(body.message)
      }
      
    }
    


  };

  const handleCancel = (event) => {
    navigate("/");
  };
  return (
    <Box maxWidth="500px" mx="auto">
      <Heading as="h1" textAlign="center" mb="8" textColor={"teal"} >
        Book an Appointment
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


        <FormControl id="email" mb="4">
          <FormLabel>Email address</FormLabel>
          <Input
            type="email"
            placeholder="Enter your email address"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
          />
        </FormControl>

        <FormControl id="receipt" mb="4">
          <FormLabel>Receipt ID</FormLabel>
          <Input
            type="text"
            placeholder="Enter your payment receipt id."
            value={receiptID}
            onChange={(event) => setReceiptID(event.target.value)}
          />
        </FormControl>
        <FormControl id="appointmentDate" mb="4">
          <FormLabel>Appointment Date</FormLabel>
          <Input
            type="date"
            placeholder="Select appointment date"
            value={appointmentDate}
            onChange={(event) => setAppointmentDate(event.target.value)}
          />
        </FormControl>
        <FormControl id="timeSlot" mb="4">
          <FormLabel>Appointment Time Slot</FormLabel>
          <Select
            placeholder="Select appointment time slot"
            value={appointmentTimeSlot}
            onChange={(event) => setAppointmentTimeSlot(event.target.value)}
          >
            <option value="10:00AM - 12:00PM">10:00AM - 12:00PM</option>
            <option value="1:00PM - 3:00PM">1:00PM - 3:00PM</option>
            <option value="4:00PM - 6:00PM">4:00PM - 6:00PM</option>
          </Select>
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
  );
}
