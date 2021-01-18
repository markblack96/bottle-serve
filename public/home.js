/**
 * Home (localhost:5000/)
 */

const PseudoComp = function (options) { // https://gomakethings.com/how-to-create-a-state-based-ui-component-with-vanilla-js/
    this.elem = document.querySelector(options.selector);
    this.data = options.data;
    this.template = options.template;
}

async function getVideoList() {
    let videoList = await fetch('/videos').then(r=>r.json())
    
    return videoList.data
}
(async ()=> {
    const app = new PseudoComp({
        selector: '#root',
        data: {
            videos: await getVideoList(),
        },
        template: function(props) {
            console.log(this.data)
            return `
                <h2>Downloads</h2>
                <ul>
                    ${props.videos.map(function (video) {
                        if (video.split('.')[video.split('.').length-1] === 'mkv') return `<li><a href="/videos/${video}">${video}</a></li>`;
                    }).join('')}
                </ul>
                <h2>Watch</h2>
                <ul>
                    <button id="buildPlaylist">Build Playlist</button>
                    ${props.videos.map(function (video) {
                        if (video.split('.')[video.split('.').length-1] === 'mp4' || video.split('.')[video.split('.').length-1] === 'webm') {
                            return `<li><a href="/video/${video}">${video}</a><input value="${video}" type="checkbox"/></li>`;
                        }
                    }).join('')}
                </ul>
            `
        }
    })
    
    PseudoComp.prototype.render = function () {
        this.elem.innerHTML = this.template(this.data)
    }
    
    app.render();

    let buildPlaylistButton = document.querySelector('#buildPlaylist');
    buildPlaylistButton.onclick = ()=>{
        let selected = document.querySelectorAll("input[type='checkbox']:checked")
        console.log([...selected].map(s=>s.value))
        sessionStorage.setItem('playlist', [...selected].map(s=>s.value).slice(1))
        window.location.replace('/video/'+[...selected].map(s=>s.value).shift())
    }

})()