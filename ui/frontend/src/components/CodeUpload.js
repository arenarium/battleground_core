import React from 'react';
import { FormGroup, ControlLabel, FormControl, HelpBlock} from 'react-bootstrap';

function FieldGroup({ id, label, help, ...props }) {
  return (
    <FormGroup controlId={id}>
      <ControlLabel>{label}</ControlLabel>
      <FormControl {...props} />
      {help && <HelpBlock>{help}</HelpBlock>}
    </FormGroup>
  );
}


const CodeUpload = ({codePreview})=>{

  return (
    <div className="CodeUpload">
      <form>
        <FormGroup
          controlId="formBasicText"
        >
          <ControlLabel>Upload Your Agent Code</ControlLabel>
          <FieldGroup
                id="formControlsFile"
                type="file"
                label="File"
                help="Example block-level help text here."
              />
          <FormControl.Feedback />
          <HelpBlock>Validation is based on string length.</HelpBlock>
        </FormGroup>
      </form>
    </div>
  )
}

export default CodeUpload;
