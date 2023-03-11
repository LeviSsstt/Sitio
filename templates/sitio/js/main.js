$(function(){
    $('.main-menu-btn').on('click', function(e){
        e.preventDefault();
        $('.main-menu-content').addClass('active');
    });
    $('.main-menu-close-btn').on('click', function(e){
        e.preventDefault();
        $('.main-menu-content').removeClass('active');
    })
});

gsap.to("#bg",{
    scrollTrigger:{
        scrub:1
    },
    scale:1.5
})
gsap.to("#man",{
    scrollTrigger:{
        scrub:1
    },
    scale:0.5
})
gsap.to("#clouds_1",{
    scrollTrigger:{
        scrub:1
    },
    x:200
})
gsap.to("#clouds_2",{
    scrollTrigger:{
        scrub:1
    },
    x:-200
})
gsap.to("#text",{
    scrollTrigger:{
        scrub:1
    },
    y:500
})
// const cardTitles = document.querySelectorAll('.card-title');

// cardTitles.forEach(title => {
//   title.addEventListener('click', () => {
//     window.open('ejemplo.cl', '_blank');
//   });
// });
function openPage(pageName) {
    window.location.href = pageName;
  }

    
    
    