//  alert('eventDetails is connected')

function EventDetails(props){
    console.log(props);
    const {eventObj, recipientObj} = props;
    const date = moment(eventObj.event_date);
    const newDate = date.format('dddd, MMM Do YYYY')
    let noteForm ;
    function handleDeleteEvent(evt){
        fetch(`/remove_event/${props.eventObj.event_id}`,{
       method:"POST",
        headers: {
            "Accept": 'application/json',
            "Content-Type":"application/json",
        }
       
        })
        .then(result => result.json())
        .then(result =>{
            window.location.reload()
        })
    }
if (eventObj.note){
   noteForm = <UpdateNote note={eventObj.note} recipientId={recipientObj.recipient_id}/>

}else{
   noteForm = <CreateNote recipientId={recipientObj.recipient_id} eventObj={eventObj}/>
}
   return(
    <>
    <h2>{eventObj.event_name}</h2>
    <h2>Start preparing for this event on: {newDate}</h2>
    <button onClick={() => handleDeleteEvent(eventObj.event_id)}>remove event</button>
    <h2>{eventObj.note ? eventObj.note.content: null}</h2>
    {noteForm}
    </>
    );
}
