// alert('updateNote is connected :-)')

function UpdateNote(props){
    const [noteText , setNoteText] = React.useState(props.note)
    const [showForm, setShowForm] = React.useState(false);
    function handleSubmit(evt){
        const data = {
            note_id: props.noteId,
            update_content: noteText
        };
        fetch("/update_note", {
            method:"POST",
            headers: {
                "Content-Type": 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(result => result.json())
        .then(result =>{
            props.handleUpdateNote(noteText)
            setShowForm(false)
        })
    }
    function handleShowForm(evt){
       setShowForm(true);
    }
    return(
    <>
        <button type="submit"className="btn btn-outline-light updat-pln my-btn" onClick={handleShowForm}>Update plan</button>
        { 
        showForm && <div>
        <textarea type="textarea" className="text-box update-inpt" name="note"placeholder="update plan" value={noteText} onChange={(evt) =>{setNoteText(evt.target.value)}} />
        <br/>
        <br/>
        <button className="btn btn-outline-light my-btn" type="submit" onClick={handleSubmit}>Submit</button>
        </div> }
        
        </>
    );
}