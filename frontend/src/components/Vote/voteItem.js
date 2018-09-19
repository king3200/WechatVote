import React, { PureComponent } from 'react';
import PropTypes from 'prop-types';
import { Button, Card, WhiteSpace, WingBlank, Grid } from 'antd-mobile';

class VoteItem extends PureComponent {
    render() {
        const { id, name, avatar_url, desc, info_url, count } = this.props;

        return (
            <div style={{ padding: '12.5px' }}>
                <img src={avatar_url} style={{ width: '75px', height: '75px' }} alt="" />
                <div style={{ color: '#888', fontSize: '14px', marginTop: '12px' }}>
                    <span>{name}</span>
                </div>
                <div><span style={{ fontSize: '30px', color: '#FF6E27' }}>35</span></div>
            </div>
        );
    }
}

VoteItem.propTypes = {
    name: PropTypes.string.required,
    avatar_url: PropTypes.string.required,
    desc: PropTypes.string.required,
    info_url: PropTypes.string,
    count: PropTypes.number
};

export default VoteItem;