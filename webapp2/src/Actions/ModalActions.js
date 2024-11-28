import { app } from '../Actions';

export function handleClose() {
    app.setState({ showModal: false, modalText: '' });
}

export function handleOpen() {
    app.setState({ showModal: true, modalText: '' });
}
