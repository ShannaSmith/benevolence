console.log('connected to jinja')
editButtons = document.querySelectorAll('.edit-note-content');
for (const button of editButtons){
    button.addEventListener('click', () =>{
        console.log('button');
        console.log(button.id)
        const view = document.querySelector('.hidden');
        view.classList.remove('hidden');

        const buttonId = button.id;
        const updateForm = document.querySelector(`#update_note_${button.id}`)
        console.log(`update_note_${button.id}`)
        console.log(updateForm)
        updateForm.addEventListener('submit', (evt) =>{
            evt.preventDefault();
            console.log('form should have been submitted')

            const newContent = document.getElementById(`update_event_note_${button.id}`).value
            const formInput = {
                update_content: newContent,
                note_id: button.id,
            };
            console.log(formInput)
            fetch('/update_note', {
                method: 'POST',
                body: JSON.stringify(formInput),
                headers: {
                    'Content-Type': 'application/json',
                },
            })
              .then((response) =>response.json())
              .then((responseJson) =>{
              document.querySelector(`note_content_${button.id}`).innerHTML = newContent;
                alert(responseJson.status);
              });
    
        } ) 

        })};
