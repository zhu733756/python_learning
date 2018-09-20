var myStyle = {
    fontSize: 100,
    color: '#ff79b6'
};

var arr= [
  <h1>oh my god!</h1>,
  <h2>lol!</h2>,
];

ReactDOM.render(
    <div>
        <h1 style={myStyle}>Hello, world!</h1>
        {/*注释...*/}
        {arr}
    </div>,
    document.getElementById('example')
)