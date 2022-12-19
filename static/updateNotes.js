console.log('connected to jinja')
editButtons = document.querySelectorAll('.edit-note-content');
console.log(editButtons);
for (const button of editButtons){
    button.addEventListener('click', (evt) =>{
        console.log('!!!!!!!!!!!!!!!!!!!!!!!!!')
        console.log( evt.target.value);
        const buttonId = evt.target.value;
        console.log(button.id)
        
        const view = document.getElementById(`update_note_${buttonId}`);
        console.log(view);
       const oldContent= document.querySelector(`#note_content${buttonId}`).innerText;
       

        view.classList.remove('hidden');
        const contentBox = document.querySelector(`#update_event_note_${buttonId}`);
        contentBox.value=oldContent;
        console.log(buttonId);
        const updateForm = document.querySelector(`#update_note_${buttonId}`)
        console.log(`update_note_${buttonId}`)
        console.log(updateForm)
        updateForm.addEventListener('submit', (evt) =>{
             evt.preventDefault();
            console.log('form should have been submitted')

            const newContent = document.getElementById(`update_event_note_${buttonId}`).value
            const formInput = {
                update_content: newContent,
                note_id: Number(buttonId),
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
                console.log('second then')
              document.querySelector(`.note_content_${buttonId}`).innerHTML = newContent;
              console.log(`change html ${newContent}`)
                alert(responseJson.status);
              });
    
        }) 
        
        })   
    };

const deleteButtons = document.querySelectorAll(".remove_recipient");
// console.log(deleteButtons)
for (const btn of deleteButtons){
    // console.log(btn)
    btn.addEventListener('click', (evt) =>{
        // console.log(evt.target.id);
        const btnId = evt.target.value;
      console.log(btnId)
        
        fetch(`/remove_recipient/${btnId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
          .then((response) =>response.json())
          .then((responseJson) =>{
          document.querySelector(`#link-${btnId}`).remove();
          document.querySelector(`#remove_recipient_${btnId}`).remove();
            alert(responseJson.status);
          });

    })
};


