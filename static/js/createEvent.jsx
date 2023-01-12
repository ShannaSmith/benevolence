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
        <div className="card text-white bg-secondary mb-3" id='evt-form' >
        <div className="card-body">
        <h5 className="card-title">Add Event</h5>       
         <form>
        <div className="form-group ">
        <label htmlFor="event_name">Enter name of the event</label>
        <input type="text" id="event_name" className="form-control" name="event_name"  placeholder="event name" value={eventText} onChange={(evt) =>{setEventText(evt.target.value)}}/>
        </div>
        <div className="form-group ">
        <label htmlFor="event_date" id="event_date" name="event_date">Enter date to begin preparing for event</label>
        <input type="date" id="event_date" className="form-control" name="event_date" placeholder="plan start date" value={eventDate} onChange={(evt) =>{setEventDate(evt.target.value)}} />
        </div>
        
        <button type="submit" className="btn btn-primary"  onClick={handleSubmit}>Submit</button>
        </form>
        </div>
        </div>
    </>
    );
}

