// alert('recipientProfile is connected!')
// TODO create component for event details

function RecipientDetails(props) {
    const {recipient, events, prompts} = props;
    // TODO build list events to render in recipient details
    const eventsList = [];
    // VS CODE didn't like "event" , so used occassion
    for (const occassion of events){
        eventsList.push(<EventDetails eventObj={occassion} key={occassion.event_id} recipientObj={recipient}></EventDetails>)
    }
    const likesList = [];
    for (const prompt of prompts){
        likesList.push(<CreateLikes prompts={prompt.prompt_name} recipient_id={recipient.recipient_id}/> )
    }
    return (
        <>
            <div id="log-out">
                <a href="/logout">Logout</a>
                </div>
                <h1>{recipient.r_name}</h1>
                <div className="sched_events" >
                <h2>Events</h2>
            </div>
            <div>
            <h2>Their Favorite Things</h2>
                {likesList} 
            </div>
            <div>
                {eventsList}
            </div>
            <div>
                <CreateEvent recipient_id={recipient.recipient_id}/>
            </div>
        </>
    );
}
fetch(`/api/recipients_profile/${recipientId}`)
.then(response => response.json())
.then(responseJson =>{
    console.log(responseJson);
    const {recipient, events} = responseJson;
    ReactDOM.render(
        <RecipientDetails 
            recipient = {recipient}
            events = {events}
        />, 
        document.querySelector('#recipient-details')
    );
});

