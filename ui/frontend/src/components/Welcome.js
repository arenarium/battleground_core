import React from 'react'
import { Jumbotron, Button } from 'react-bootstrap';
import {LinkContainer} from 'react-router-bootstrap'


const Welcome = () =>(
  <div className="container">

  <Jumbotron>
  <h2>Build,  Deploy,  Win.</h2>
  <p>Collaborative game-building and computer player proving ground.</p>
  <LinkContainer to="/games">
  <Button>
    Observe Games
</Button>
</LinkContainer> or <Button>Join</Button>
  </Jumbotron>
  </div>
)

export default Welcome
