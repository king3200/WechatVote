import React, { Component } from 'react';
import { Flex } from 'antd-mobile';

class Index extends Component {
    render() {
        return (
            <div>
                <Flex justify='center' style={{'alignContent': 'center'}}>
                    欢迎访问重庆市12320投票系统
                    加载中...
                </Flex>
            </div>
        );
    }
}

export default Index;