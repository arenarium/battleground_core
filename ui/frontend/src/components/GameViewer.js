import React from 'react'
import { Grid, Row,Col,Panel, PageHeader } from 'react-bootstrap';
import VisibleGameIndex from '../containers/VisibleGameIndex'
import VisibleGameState from '../containers/VisibleGameState'
import 'whatwg-fetch'


 const GameViewer =() => (
  <div className="container">
    <Grid>
      <Row>
        <PageHeader><small>Watch and Learn from ongoing games or replays</small></PageHeader>
      </Row>
      <Row>
        <Col md={3}>
          <Panel>
            <VisibleGameIndex/>
          </Panel>
        </Col>
        <Col md={8}>
          <Panel>
            <VisibleGameState/>
          </Panel>
        </Col>
      </Row>
    </Grid>
  </div>
)

export default GameViewer
