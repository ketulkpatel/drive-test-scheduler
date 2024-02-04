import React from "react";
import { useNavigate } from "react-router-dom";
import { Button, Center, Heading, Divider } from "@chakra-ui/react";

export default function Home() {
  const navigate = useNavigate();

  const bookAppointmentOnClick = () => {
    navigate("/book-appointment");
  };
  const cancelAppointmentOnClick = () => {
    navigate("/cancel-appointment");
  };
  const reScheduleAppointmentOnClick = () => {
    navigate("/reschedule-appointment");
  };
  const viewAppointmentOnClick = () => {
    navigate("/view-appointment");
  };
  return (
    <div>
      <Center>
      <Heading textColor={"teal"}>
        Road test appointment home page!
        </Heading>

        
        </Center>

        <Center pt="10" gap="10">
        <Button
          variant="outline"
          colorScheme="teal"
          onClick={bookAppointmentOnClick}
        >
          Book appointment{" "}
        </Button>
        <Button
          variant="outline"
          colorScheme="teal"
          onClick={cancelAppointmentOnClick}
        >
          Cancel appointment{" "}
        </Button>
        <Button
          variant="outline"
          colorScheme="teal"
          onClick={reScheduleAppointmentOnClick}
        >
          Reschuedule appointment{" "}
        </Button>
        <Button
          variant="outline"
          colorScheme="teal"
          onClick={viewAppointmentOnClick}
        >
          View appointment{" "}
        </Button>
   </Center>
    </div>
  );
}
