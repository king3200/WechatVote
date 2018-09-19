import React, { Component } from 'react';
import { Grid, Modal, NavBar, NoticeBar } from 'antd-mobile';
import axios from 'axios';
import './index.css';

class VotePage extends Component {

    constructor(props) {
        super(props);
        this.state = {
            projId: undefined,
            voteName: '',
            startDate: '',
            endDate: '',
            dataArray: [],
            isVoted: false,
            modalShow: false,
            modalValue: {}
        }
    }

    componentDidMount() {
        axios.get('http://127.0.0.1:8000/retrive/3')
            .then(response => response.data)
            .then(data => {
                console.log(data);
                this.setState({ projId: data['id'], voteName: data['name'], startDate: data['start_date'], endDate: data['end_date'], dataArray: data['items'] })
            });
    }

    onGridClick = (data) => {
        console.log(data);
        this.setState({modalShow: true, modalValue: data});
        
    }

    onClose = () => {
        this.setState({modalShow: false});
    }

    onVote = () => {
        console.log(this.state.modalValue);
        axios.post('http://127.0.0.1:8000/voting', {projId: this.state.projId, id:this.state.modalValue.id})
            .then(response => response.status)
            .then(status => {
                Modal.alert('投票成功');
                const id = this.state.modalValue.id;
                const newArray = [...this.state.dataArray]
                console.log(newArray);
                newArray.forEach((val, index) => {
                    if(val.id === id){
                        val.counter += 1;
                    }
                });
                this.setState({ modalShow: false, dataArray: newArray})
            }).catch(err => {
                console.log(err);
                console.log(err.response);
                Modal.alert('错误:' + err.response.data.detail);
            })
    }

    render() {

        const GridItem = dataItem => (
            <div style={{ padding: '12.5px' }} key={dataItem.id}>
                <img src={dataItem.avatar_url} style={{ width: '100px', height: '100px' }} alt="" />
                <div style={{ color: '#888', fontSize: '14px', marginTop: '12px' }}>
                    <span>{dataItem.name}</span>
                </div>
                <br />
                <div><span style={{ fontSize: '16px', color: '#FF6E27' }}>得票数：{dataItem.counter}</span></div>
            </div>
        )
        console.log(this.state.dataArray)
        return (
            <div>

            <NavBar>重庆医生视频大赛投票系统</NavBar>
            <NoticeBar>点击单个窗口了解详情</NoticeBar>

                <Grid
                    data={this.state.dataArray}
                    columnNum={2}
                    renderItem={GridItem}
                    onClick={this.onGridClick}
                />

                <Modal
                    visible={this.state.modalShow}
                    transparent
                    maskClosable={false}
                    title={this.state.modalValue.title}
                    footer={[{ text: '投他一票', onPress: () => { this.onVote(); } }, { text: '关闭', onPress: () => { this.onClose(); } }]}
                    wrapProps={{ onTouchStart: this.onWrapTouchStart }}
                    className={'web'}
                    // wrapClassName={'web'}
                >
                    <div style={{ height: '600px', overflow: 'scroll', width: '100%' }}>
                        <h2>{this.state.modalValue.name}</h2>
                        <p>{this.state.modalValue.desc}</p>
                    </div>
                </Modal>
            </div>
        );
    }
}

export default VotePage;