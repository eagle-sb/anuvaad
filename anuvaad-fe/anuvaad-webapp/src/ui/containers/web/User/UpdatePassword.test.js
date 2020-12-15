import React from 'react';
import { configure, shallow, mount } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import { UpdatePassword } from './UpdatePassword';
import Button from "@material-ui/core/Button";
import { jssPreset } from '@material-ui/core';
import APITransport from "../../../../flux/actions/apitransport/apitransport";

configure({ adapter: new Adapter() })
function onsubmit() {
    console.log('==============test==============')
}
describe('<UpdatePassword/>', () => {

    it("fields check", () => {
        const wrapper = shallow(<UpdatePassword />);
        // wrapper.find('TextField[type="email"]');
        wrapper.find('#email')
        wrapper.find('#submit')
        expect(wrapper);
    })

    it("Button check", () => {
        const mockCallBack = jest.fn();
        const wrapper = shallow(<UpdatePassword onClick={mockCallBack}/>);
        wrapper.find('button').simulate('click', { preventDefault: jest.fn(), stopPropagation: jest.fn() });
        expect(wrapper)
    })

   


    it("Cred check", () => {
        const mockCallBack = jest.fn();
        const wrapper = shallow(<UpdatePassword APITransport={mockCallBack}/>);
        
        wrapper.find('#email').simulate('change', { target: { value: 'meghana.msa@gmail.com' } })
        wrapper.find('button').simulate('click', { preventDefault: jest.fn(), stopPropagation: jest.fn() });
       
        expect(wrapper)
    })


})
