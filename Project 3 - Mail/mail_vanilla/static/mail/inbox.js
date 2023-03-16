document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').addEventListener('submit', sumbit_email);
  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function sumbit_email(e)
{
  e.preventDefault()

  const form = document.querySelector('#compose-form');
  const formData = new FormData(form);
  const obj = Object.fromEntries(formData)

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: obj.To,
        subject: obj.Subject,
        body: obj.Body
    })
  })
  .then(response =>
  {
    console.log(response)
    if (response.status == 400)
      alert('nah man')
    else 
      load_mailbox('sent')
  })

  
}



function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
    // Print emails
    console.log(emails);
    
    // for each email in emails create a div with the sender, subject, body, timestamp, and if it's been read or not
    // and append it to the emails-view div
    emails.forEach(email => {
      const div = document.createElement('div')
      div.innerHTML =`<div class="card">
                        <h5 class="card-title">${email.sender}</h5>
                        <h6 class="card-subtitle mb-2 text-muted">${email.subject}</h6>
                        <div class="card-body">${email.body}</div>
                        <div class="card-footer">${email.timestamp}</div>
                      </div>`
      document.querySelector('#emails-view').append(div)
    });
  });
}
