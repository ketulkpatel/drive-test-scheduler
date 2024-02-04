import React, { useState, useEffect } from "react";
import { Box, Heading, Text } from "@chakra-ui/react";
import { useLocation } from "react-router-dom";

export default function AppoinmentDetails() {

  const {state} = useLocation();

  return (
    <Box maxWidth="500px" mx="auto" mt="8">
      <Heading as="h1" textAlign="center" mb="8">
        Appointment Details
      </Heading>
      <Box bg="gray.100" p="4" rounded="md" mb="4">
        <Text>
          <strong>License Number:</strong> {state.data.license_number}
        </Text>
        <Text>
          <strong>Date of Birth:</strong> {state.data.date_of_birth}
        </Text>
        <Text>
          <strong>Appointment ID:</strong> {state.data.appointment_id}
        </Text>
        <Text>
          <strong>Email:</strong> {state.data.email_address}
        </Text>
        <Text>
          <strong>Appointment Date:</strong> {state.data.appointment_date}
        </Text>
        <Text>
          <strong>Appointment Time Slot:</strong>{" "}
          {state.data.appointment_slot}
        </Text>
      </Box>
    </Box>
  );
}
