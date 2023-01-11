// alert('recipientProfile is connected!')
function RecipientDetails(props) {
    console.log('rendering recip profile>>>')
    const {recipient, events, prompts, likes} = props;
    const [eventsState, setEventsState] = React.useState(events)
    console.log('props printout>>>>>>>>',props)
    const eventsList = [];
    // VS CODE didn't like "event" , so used occassion
    for (const occassion of eventsState){
        console.log('occassionId>>>>', occassion.event_id)
        eventsList.push(<EventDetails eventObj={occassion} key={occassion.event_id} recipientObj={recipient}/>)
    }

    function handleNewEvent(newEvent){
        setEventsState(existingEvents => [...existingEvents, newEvent])
    }
    const promptsList = [];
    for  (const prompt of prompts){
        promptsList.push(<CreateLike prompt={prompt} key={prompt.prompt_id} recipient_id={recipient.recipient_id}/>)
    }
    const likesList = [];
    for (const like of likes){
        likesList.push(<div key={like.like_id}>
            {like.like_name} 
        </div>)
    }
    return (
        <>
            <div id="log-out">
                <a href="/logout">Logout</a>
                </div>
                <h2>{recipient.r_name}</h2>
                <div className="sched_events" >
                <h3>Events</h3>
                
                {eventsList}
                 </div>
            <div>
            <h3>Their Favorite Things</h3>
                {likesList} 
            </div>
            <div>
                
                {promptsList}
            </div>
           
            <div>
                <CreateEvent recipient_id={recipient.recipient_id} handleNewEvent={handleNewEvent} />
            </div>
            <div>
                {/* <CreateLike recipient_id={recipient.recipient_id} handleNewLike={handleNewLike}/> */}
            </div>
        </>
    );
}

fetch(`/api/recipients_profile/${recipientId}`)
.then(response => response.json())
.then(responseJson =>{
    console.log(responseJson);
    const {recipient, events, prompts,likes} = responseJson;
    ReactDOM.render(
        <RecipientDetails 
            recipient = {recipient}
            events = {events}
            prompts = {prompts}
            likes = {likes}
        />, 
        document.querySelector('#recipient-details')
    );
});

