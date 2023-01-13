// alert('createNote is connected :~)')

function CreateNote(props){
    const [noteText, setNoteText] = React.useState("")
    const [removeForm, setRemoveForm] =React.useState(true)
        function handleSubmit(evt){
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
                console.log(' result>>>>>>', result)
                props.handleNewNote(result.content, result.note_id)
                setRemoveForm(false);
                
            })

        }
    return(
    <>
        { 
        removeForm && <div>
        
        {/* <label htmlFor="note"></label> */}
        <textarea class="form-control" placeholder="Enter your plan" type="textarea" rows="3" name="note" value={noteText} onChange={(evt) =>{setNoteText(evt.target.value)}}></textarea>
        <button className="btn btn-outline-light" type="button" onClick={handleSubmit}>Submit</button>
        </div>}
    </>
    );
}