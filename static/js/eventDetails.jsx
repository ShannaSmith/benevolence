// alert('eventDetails is connected')
function EventDetails(props){
    console.log(props);
    const {eventObj}= props;
//    const eventList = eventD.map((event) =>
//    <li>{event}</li>
//    );
   return(
    <>
    <h2>{eventObj.event_name}</h2>
    <h2>{eventObj.event_date}</h2>
    <h2>{eventObj.note ? eventObj.note.content: null}</h2>
    </>
    );
}
