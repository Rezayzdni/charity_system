import React from 'react'
import Navbar from '../Components/Navbar'
import { Button, Col, Form } from 'react-bootstrap'
import axios from 'axios';

export default class BenefactorProfile extends React.Component {
    state = {
        fields: {
            firstname: '',
            lastname: '',
            phone: '',
            email: '',
            address: '',
            description: '',
            gender: '',
            age: '',
            experience: '',
            freeTime: ''
        }
    }

    componentDidMount() {
        const token = window.localStorage.getItem('token');
        axios.get('http://localhost:8000/api/user-benefactor-fields/', {
            headers: {
                'Authorization': `Token ${token}`
            }
        })
        .then((response) => {
            const user = response.data.user; // Assuming the first user is relevant
            const benefactor = response.data.benefactor;

            // Map experience level
            let experienceLevel = '';
            if (benefactor.experience === 0) {
                experienceLevel = '0';
            } else if (benefactor.experience === 1) {
                experienceLevel = '1';
            } else if (benefactor.experience === 2) {
                experienceLevel = '2';
            }

            this.setState({
                fields: {
                    firstname: user.first_name || '',
                    lastname: user.last_name || '' ,
                    phone: user.phone || '',
                    email: user.email || '' ,
                    address: user.address || '',
                    description: user.description || '',
                    gender: user.gender || '',
                    age: user.age || '',
                    experience: experienceLevel, // Set mapped experience level
                    freeTime: benefactor.free_time_per_week || ''
                }
            });
            console.log('free time:', benefactor.free_time_per_week);
            console.log('user experience:', experienceLevel);
        })
        .catch((error) => {
            console.error('Error fetching user fields:', error);
        });
    }

    handleChange(event) {
        const name = event.target.name
        const changeFields = this.state.fields
        changeFields[name] = event.target.value
        this.setState({ fields: changeFields })
    }

    handleSubmit(event) {
        event.preventDefault(); // Prevent default form submission

        const token = window.localStorage.getItem('token');
        const data = this.state.fields; // Get the fields from the state

        axios.put('http://localhost:8000/api/user-benefactor-fields/', data, {
            headers: {
                'Authorization': `Token ${token}`,
                'Content-Type': 'application/json'
            }
        })
        .then((response) => {
            console.log('Data updated successfully:', response.data);
            alert('اطلاعات با موفقیت به‌روزرسانی شد');
        })
        .catch((error) => {
            console.error('Error updating data:', error);
            alert('خطا در به‌روزرسانی اطلاعات');
        });
    }

    render() {
        return (
            <div>
                <Navbar />
                <div className='bene-container'>
                    <div className='demographic-container' dir='rtl'>
                        <h2 style={{ alignSelf: 'right', marginBottom: '10px' }}>
                            اطلاعات نیکوکار
                        </h2>
                        <Form>
                            <Form.Row>
                                <Col>
                                    <Form.Label>نام</Form.Label>
                                    <Form.Control name='firstname'
                                        placeholder='نام خود را وارد نمایید'
                                        value={this.state.fields.firstname}
                                        onChange={(event) => this.handleChange(event)} />
                                </Col>
                                <Col>
                                    <Form.Label>نام خانوادگی</Form.Label>
                                    <Form.Control name='lastname'
                                        placeholder='نام خانوادگی خود را وارد نمایید'
                                        value={this.state.fields.lastname}
                                        onChange={(event) => this.handleChange(event)} />
                                </Col>
                            </Form.Row>
                            <Form.Row>
                                <Col>
                                    <Form.Label> جنسیت </Form.Label>
                                    <Form.Control as='select' name='gender'
                                        value={this.state.fields.gender || 'MF'}
                                        onChange={(event) => this.handleChange(event)}>
                                        <option value='MF'>هیچکدام</option>
                                        <option value='F'>زن</option>
                                        <option value='M'>مرد</option>
                                    </Form.Control>
                                </Col>
                                <Col>
                                    <Form.Label> سن </Form.Label>
                                    <Form.Control type='number' name='age'
                                        placeholder='سن خود را وارد نمایید'
                                        value={this.state.fields.age}
                                        onChange={(event) => this.handleChange(event)}
                                    />
                                </Col>
                            </Form.Row>
                            <Form.Row>
                                <Col>
                                    <Form.Label>ایمیل</Form.Label>
                                    <Form.Control name='email'
                                        placeholder='ایمیل خود را وارد نمایید'
                                        value={this.state.fields.email}
                                        onChange={(event) => this.handleChange(event)}
                                    />
                                </Col>
                                <Col>
                                    <Form.Label> شماره تماس </Form.Label>
                                    <Form.Control
                                        placeholder=' شماره تماس خود را وارد نمایید'
                                        name='phone'
                                        value={this.state.fields.phone}
                                        onChange={(event) => this.handleChange(event)}
                                    />
                                </Col>
                            </Form.Row>
                            <Form.Row>
                                <Col>
                                    <Form.Label> آدرس </Form.Label>
                                    <Form.Control name='address'
                                        placeholder='آدرس خود را وارد نمایید'
                                        value={this.state.fields.address}
                                        onChange={(event) => this.handleChange(event)}
                                    />
                                </Col>
                            </Form.Row>
                            <Form.Row>
                                <Col>
                                    <Form.Label> تجربه نیکوکاری </Form.Label>

                                    <Form.Control as='select' name='experience'
                                                                            value={this.state.fields.experience || ''} // Ensure empty string if null
                                                                            onChange={(event) => this.handleChange(event)}>
                                                                            <option value='0'>تازه‌کار</option>
                                                                            <option value='1'>متوسط</option>
                                                                            <option value='2'>حرفه‌ای</option>
                                                                        </Form.Control>
                                </Col>
                                <Col>
                                    <Form.Label> زمان آزاد در هفته </Form.Label>
                                    <Form.Control name='freeTime'
                                        type='number'
                                        placeholder='20'
                                        value={this.state.fields.freeTime}
                                        onChange={(event) => this.handleChange(event)}
                                    />
                                </Col>

                            </Form.Row>
                            <Form.Row>
                                <Col sm='12'>
                                    <Form.Group controlId='exampleForm.ControlTextarea1'>
                                        <Form.Label>توضیحات</Form.Label>
                                        <Form.Control as='textarea' rows='3'
                                            name='description'
                                            value={this.state.fields.description}
                                            onChange={(event) => this.handleChange(event)}
                                        />
                                    </Form.Group>
                                </Col>
                            </Form.Row>
                            <Form.Row>
                                <Col sm='5'></Col>
                                <Col>
                                    <Button type='submit' onClick={(event) => this.handleSubmit(event)}> ثبت اطلاعات </Button>
                                </Col>
                                <Col sm='8'></Col>
                            </Form.Row>
                        </Form>
                    </div>
                </div>
            </div>
        )
    }
}
