// alert('createNote is connected :~)')
function CreateNote(props){
    const [noteText, setNoteText] = React.useState("")
    const [removeForm, setRemoveForm] =React.useState(true)
        function handleSubmit(evt){
            const [showForm, setShowForm] = React.useState(false)
            console.log('noteText>>>>>>>>',noteText)
            const data = {note:noteText};
            fetch(`/note/new/${props.eventObj.event_id}`, {
                method:"POST",
                headers: {
                    "content-Type": 'application/json'
                },
                body:JSON.stringify(data)
            })
            .then(result => result.json())
            .then(result =>{
                console.log(`Ajax call for create Note returned this:${result}`)
                // window.location.reload()
                props.handleNewNote(noteText)
                setShowForm(true);
                setRemoveForm(false);
            })
        }
    return(
    <>
        { 
        removeForm && <div>
        <h4>Create your plan</h4>
        <label htmlFor="note">Create your plan here</label>
        <input type="textarea" name="note" value={noteText} onChange={(evt) =>{setNoteText(evt.target.value)}} />
        <br/>
        <br/>
        <input type="submit" onClick={handleSubmit} value="Submit"/>
        </div>}
    </>
    );
}