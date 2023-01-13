// alert('createLikes is :-)')
function CreateLike(props){
    console.log('print props>>>>>>', props);
    const [like, setLikeText] = React.useState("");
    const [user_answer, setUserAnswer] = React.useState("");
console.log('print out of props.prompt>>>>>>>>>>', props.prompt)

    function handleSubmit(evt){
        console.log('New like>>>>>>>>>>', like);
        console.log('prompt_id>>>>>>>>>>>', props.prompt.prompt_id);
        const data = {
             prompt_id:props.prompt.prompt_id,
             user_answer:user_answer,
            like:like,
            recipient_id:props.recipient_id
        };
        console.log('print recipient>>>>>>>>>>', props.recipient_id)
        fetch(`/likes/new/${props.recipient_id}`, {
            method:"POST",
            headers: {
                "Content-Type": 'application/json'
            },
            body:JSON.stringify(data)
        })
        .then(result => result.json())
        .then(result =>{
            console.log(`Ajax call for create event returned this: ${result}`)
            window.location.reload()
        })
    }
    return(
    <>
    
    <div>   
    <div className="input-group mb-3 promt-inpt "> 
        {/* <label htmlFor="prompt_reply" className="likes ">{props.prompt.prompt_name}</label> */}
        <input type="text" name="prompt_reply" className="form-control likes" placeholder={props.prompt.prompt_name} value={user_answer} onChange={(evt) =>{setUserAnswer(evt.target.value)}} />
        <input type="hidden" name="prompt_id" className="form-control" value={props.prompt.prompt_id} />    
        <button  value="Add interest"className="btn btn-outline-secondary" type="submit" id="button-addon2" onClick={handleSubmit}>Submit</button>
       </div>
    </div>
    </>
    );   
}