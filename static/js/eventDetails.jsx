//  alert('eventDetails is connected')

function EventDetails(props){
    console.log(props);
    const {eventObj, recipientObj} = props;
    const [noteContent, setNoteContent] = React.useState(eventObj.note ? eventObj.note.content: null)
    const [noteId, setNoteId] = React.useState(eventObj.note ? eventObj.note.note_id: null)
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
   function handleUpdateNote(updatedNoteText){
    setNoteContent(updatedNoteText)
   }
   function handleNewNote(newNoteText, newNoteId){
    setNoteContent(newNoteText)
    setNoteId(newNoteId)

   }
if (noteContent != null){
   noteForm = <UpdateNote note={noteContent} 
    recipientId={recipientObj.recipient_id} 
    handleUpdateNote={handleUpdateNote}
    noteId={noteId}/>

}else{
   noteForm = <CreateNote recipientId={recipientObj.recipient_id} 
    eventObj={eventObj} handleNewNote={handleNewNote} 
    handleUpdateNote={handleUpdateNote} />
}
   return(
    <>
    <h2>{eventObj.event_name}</h2>
    <h2>Start preparing for this event on: {newDate}</h2>
    <button onClick={() => handleDeleteEvent(eventObj.event_id)}>remove event</button>
    <h2>{noteContent}</h2>
    {noteForm}
    </>
    );
}
