// alert('recipientProfile is connected!')
function RecipientDetails(props) {
  console.log("rendering recip profile>>>");
  const { recipient, events, prompts, likes } = props;
  const [eventsState, setEventsState] = React.useState(events);
  console.log("props printout>>>>>>>>", props);
  const eventsList = [];
  // VS CODE didn't like "event" , so used occassion
  for (const occassion of eventsState) {
    console.log("occassionId>>>>", occassion.event_id);
    eventsList.push(
      <EventDetails
        eventObj={occassion}
        key={occassion.event_id}
        recipientObj={recipient}
      />
    );
  }

  function handleNewEvent(newEvent) {
    setEventsState((existingEvents) => [...existingEvents, newEvent]);
  }
  const promptsList = [];
  for (const prompt of prompts) {
    promptsList.push(
      <CreateLike
        prompt={prompt}
        key={prompt.prompt_id}
        recipient_id={recipient.recipient_id}
      />
    );
  }
  const likesList = [];
  for (const like of likes) {
    likesList.push(<div key={like.like_id}>{like.like_name}</div>);
  }
  return (
    <>
      <h2 className="r-name">{recipient.r_name}</h2>
      <div className="sched_events">
        <div className="profle-pg">
          <div id="evt-thgs">
            <div id="fav-thgs">
              <div className="card" id="like-card">
                <div className="card-header">Favorites</div>
                <div className="card-body">
                  <div className="card-text text-box ">{likesList}</div>
                </div>
              </div>
            </div>

            <CreateEvent
              recipient_id={recipient.recipient_id}
              handleNewEvent={handleNewEvent}
            />
          </div>

          <div className="card-deck">{eventsList}</div>
        </div>
      </div>
      <div id="prompts">{promptsList}</div>
    </>
  );
}

fetch(`/api/recipients_profile/${recipientId}`)
  .then((response) => response.json())
  .then((responseJson) => {
    console.log(responseJson);
    const { recipient, events, prompts, likes } = responseJson;
    ReactDOM.render(
      <RecipientDetails
        recipient={recipient}
        events={events}
        prompts={prompts}
        likes={likes}
      />,
      document.querySelector("#recipient-details")
    );
  });
