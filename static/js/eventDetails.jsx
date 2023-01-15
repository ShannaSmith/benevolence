//  alert('eventDetails is connected')

function EventDetails(props) {
  console.log(props);
  const { eventObj, recipientObj } = props;
  const [noteContent, setNoteContent] = React.useState(
    eventObj.note ? eventObj.note.content : null
  );
  const [noteId, setNoteId] = React.useState(
    eventObj.note ? eventObj.note.note_id : null
  );
  const date = moment.utc(eventObj.event_date);
  console.log('date>>>>>',date)
  
  const newDate = date.format("dddd, MMM Do YYYY");
  console.log('newDate>>>>>', newDate)
  let noteForm;
  function handleDeleteEvent(evt) {
    fetch(`/remove_event/${props.eventObj.event_id}`, {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
    })
      .then((result) => result.json())
      .then((result) => {
        window.location.reload();
      });
  }
  function handleUpdateNote(updatedNoteText) {
    setNoteContent(updatedNoteText);
  }
  function handleNewNote(newNoteText, newNoteId) {
    setNoteContent(newNoteText);
    setNoteId(newNoteId);
  }
  if (noteContent != null) {
    noteForm = (
      <UpdateNote
        note={noteContent}
        recipientId={recipientObj.recipient_id}
        handleUpdateNote={handleUpdateNote}
        noteId={noteId}
      />
    );
  } else {
    noteForm = (
      <CreateNote
        recipientId={recipientObj.recipient_id}
        eventObj={eventObj}
        handleNewNote={handleNewNote}
        handleUpdateNote={handleUpdateNote}
      />
    );
  }
  return (
    <>
        <div className="card profile-card m-3">
          <div className="card-header">Event</div>
          <div className="card-body">
            <h5 className="card-title">{eventObj.event_name}</h5>
            <p className="card-text">Begin prep : {newDate}</p>
            <button
              className="btn btn-outline-light my-btn"
              onClick={() => handleDeleteEvent(eventObj.event_id)}
            >
              remove event
            </button>

            <div>
              <div className="header">Plan:</div>
              <p className="card-text">{noteContent}</p>
              {noteForm}
            </div>
            <div className="card-footer">
      <small className="text-muted">Share Kindness</small>
    </div>
          </div>
        </div>
    </>
  );
}
