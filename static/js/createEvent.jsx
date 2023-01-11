// alert('createEvent is connected ;~)')
function CreateEvent(props){
    const [eventText, setEventText ] = React.useState("");
    const [eventDate, setEventDate] = React.useState("");
    function handleSubmit(evt){
        console.log('eventText>>>>>>>>>>>>>>>', eventText);
        console.log('eventDate>>>>>>>>>>>>>>>', eventDate);
        const data = {
            event_name:eventText,
            event_date:eventDate,
            event_id:""
        };
        fetch(`/recipients/${props.recipient_id}/events`, {
            method:"POST",
            headers: {
                "content-Type": 'application/json'
            },
            body:JSON.stringify(data)
        })
        .then(result => result.json())
        .then(result =>{
            console.log('Ajax call for create event returned this:', result)
            // window.location.reload()
            props.handleNewEvent(result)
            setEventText('')
            setEventDate('')
        })
    }
    return(
    <>
        <h3>Add Events</h3>
        <label htmlFor="event_name">Enter the name of the event</label>
        <input type="text" id="event_name" name="event_name" value={eventText} onChange={(evt) =>{setEventText(evt.target.value)}}/>
        <br/>
        <br/>
        <label htmlFor="event_date" id="event_date" name="event_date">Enter date to begin preparing for event</label>
        <input type="date" id="event_date" name="event_date" value={eventDate} onChange={(evt) =>{setEventDate(evt.target.value)}} />
        <br/>
        <br/>
        <input type="submit" value="Submit" onClick={handleSubmit}/>

    </>
    );
}