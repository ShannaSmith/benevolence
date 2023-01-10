// alert('recipientProfile is connected!')
function RecipientDetails(props) {
    const {recipient, events, prompts, likes} = props;

    console.log('props printout>>>>>>>>',props)
    const eventsList = [];
    // VS CODE didn't like "event" , so used occassion
    for (const occassion of events){
        eventsList.push(<EventDetails eventObj={occassion} key={occassion.event_id} recipientObj={recipient}></EventDetails>)
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
                <h3>Add Interest</h3>
                {promptsList}
            </div>
           
            <div>
                <CreateEvent recipient_id={recipient.recipient_id} />
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

