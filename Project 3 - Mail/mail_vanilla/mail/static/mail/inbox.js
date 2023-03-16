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
  document.querySelector('#email-view').style.display = 'none';

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
  document.querySelector('#email-view').style.display = 'none';

  const title = document.createElement('h3')

  if (mailbox == 'archive') {
    title.innerHTML = `<h3>📦 ${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  }
  else if (mailbox == 'inbox'){
    title.innerHTML = `<h3>📬 ${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  }
  else if (mailbox == 'sent'){
    title.innerHTML = `<h3>📤 ${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  }

  document.querySelector('#emails-view').innerHTML = title.innerHTML;


  fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
    
    // for each email in emails create a div with the sender, subject, body, timestamp, and if it's been read or not
    // and append it to the emails-view div
    emails.forEach(email => {
      if (mailbox == 'inbox' && !email.archived){
        const div = generate_email_html(email, mailbox);
        document.querySelector('#emails-view').append(div);
      }
      else
      {
        const div = generate_email_html(email, mailbox);
        document.querySelector('#emails-view').append(div);
      }
    });
  });
}

function generate_email_html(email, mailbox)
{
  const div = document.createElement('div')
  // if the email is read, make the background grey, otherwise make it white
  let color = email.read ? 'blue' : 'red';
  

  div.innerHTML =`<div class="card" id=email_${email.id}>
                    <h5 class="card-title" style="color: ${color}">${email.sender}</h5>
                    <a href="javascript: load_email(${email.id})"><h6 class="card-subtitle mb-2 text-muted">${email.subject}</h6></a>
                    <div class="card-body">${email.body}</div>
                    <div class="card-footer">
                      ${email.timestamp}
                      <button class="btn btn-primary" onclick="archive_email(${email.id})">${mailbox === 'archive' ? 'Unarchive' : 'Archive'}</button>
                    </div>
                  </div>`
  // if mailbox is email then add a reply button
  if (mailbox === 'email')
  {
    const reply_button = document.createElement('button')
    reply_button.className = 'btn btn-primary'
    reply_button.innerHTML = 'Reply'
    reply_button.onclick = () => reply_email(email)
    div.querySelector('.card-footer').append(reply_button)
  }
  return div;
}

function load_email(id)
{
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {

  const div = generate_email_html(email, 'email');

  document.querySelector('#email-view').innerHTML = '';
  document.querySelector('#email-view').append(div);
  
  // show the email-view div and other views
  document.querySelector('#email-view').style.display = 'block';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // send a PUT request to mark the email as read
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  })


  });

}

function archive_email(id)
{
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
    fetch(`/emails/${id}`, {
      method: 'PUT',
      body: JSON.stringify({
          archived: !email.archived
      })
    }).then(() => load_mailbox('inbox'))
  })
}

function reply_email(email)
{
  compose_email()
  document.querySelector('#compose-recipients').value = email.sender;
  document.querySelector('#compose-subject').value = 'Re: ' + email.subject;
  document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote: "${email.body}"`;

}