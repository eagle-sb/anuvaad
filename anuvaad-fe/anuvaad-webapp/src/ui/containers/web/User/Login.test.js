import { render, fireEvent } from '@testing-library/react';
import React from 'react';
import { queryByAttribute } from '@testing-library/react';
import Login from './Login.jsx';
import { BrowserRouter as Router } from "react-router-dom";
import { Provider } from 'react-redux';
import storeFactory from '../../../../flux/store/store';

const getById = queryByAttribute.bind(null, 'id');
describe('<Login />', () => {
    test('check if email and password node is present', () => {
        const component = render(<Provider store={storeFactory}><Router><Login /></Router></Provider>);
        const emailNode = getById(component.container, 'email');
        const passwordNode = getById(component.container, 'passowrd');
        console.log(emailNode, passwordNode);
    });
})