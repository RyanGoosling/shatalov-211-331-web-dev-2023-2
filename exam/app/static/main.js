'use strict';

function imagePreviewHandler(event) {
    if (event.target.files && event.target.files[0]) {
        let reader = new FileReader();
        reader.onload = function (e) {
            let img = document.querySelector('.background-preview > img');
            img.src = e.target.result;
            if (img.classList.contains('d-none')) {
                let label = document.querySelector('.background-preview > label');
                label.classList.add('d-none');
                img.classList.remove('d-none');
            }
        }
        reader.readAsDataURL(event.target.files[0]);
    }
}

function openLink(event) {
    if (event.target.tagName == 'I' || event.target.closest('.card') == null) 
        return;
    let card = event.target.closest('.card');
    if (card.dataset.url) {
        window.location = card.dataset.url;
    }
}

function deleteBookHandler(event) {
    let form = document.querySelector('form');
    form.action = event.relatedTarget.dataset.url;
    let bookName = document.querySelector('#bookName');
    // console.log(event.relatedTarget.closest('.card'))
    bookName.innerHTML = event.relatedTarget.closest('.card').querySelector('#nameOfBook').textContent;
}



window.onload = function() {
    let deleteUserModal = document.querySelector('#deleteBook');
    if (deleteUserModal) {
        deleteUserModal.addEventListener('show.bs.modal', deleteBookHandler);
    }

    let book_desc = document.getElementById('short_desc');
    if (book_desc) {
        const easymde = new EasyMDE({book_desc},);
    }

    let review_text = document.getElementById('review-text');
    if (review_text) {
        const easymde = new EasyMDE({review_text},);
    }

    let background_img_field = document.getElementById('background_img');
    if (background_img_field) {
        background_img_field.onchange = imagePreviewHandler;
    }
    for (let course_elm of document.querySelectorAll('.courses-list .col-md-4')) {
        course_elm.onclick = openLink;
    }
    for (let course_elm of document.querySelectorAll('.recent-book')) {
        course_elm.onclick = openLink;
    }
}