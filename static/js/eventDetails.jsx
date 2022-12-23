// alert('eventDetails is connected')
function EventDetails(props){
    console.log(props);
    const {eventObj, recipientObj} = props;
    
//    const eventList = eventD.map((event) =>
//    <li>{event}</li>
//    );
let noteForm ;
if (eventObj.note){
   noteForm = <UpdateNote note={eventObj.note} recipientId={recipientObj.recipient_id}/>

}else{
   noteForm = <p>create note form coming soon</p>
}
   return(
    <>
    <h2>{eventObj.event_name}</h2>
    <h2>{eventObj.event_date}</h2>
    <h2>{eventObj.note ? eventObj.note.content: null}</h2>
    {noteForm}
    </>
    );
}
