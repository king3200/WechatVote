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
        axios.get('/retrive/1')
            .then(response => response.data)
            .then(data => {
                this.setState({ projId: data['id'], voteName: data['name'], startDate: data['start_date'], endDate: data['end_date'], dataArray: data['items'] })
            });
    }

    onGridClick = (data) => {
        this.setState({modalShow: true, modalValue: data});
        
    }

    onClose = () => {
        this.setState({modalShow: false});
    }

    onVote = () => {
        axios.post('/voting', {projId: this.state.projId, id:this.state.modalValue.id})
            .then(response => response.status)
            .then(status => {
                Modal.alert('投票成功');
                const id = this.state.modalValue.id;
                const newArray = [...this.state.dataArray]
                newArray.forEach((val, index) => {
                    if(val.id === id){
                        val.counter += 1;
                    }
                });
                this.setState({ modalShow: false, dataArray: newArray})
            }).catch(err => {
                this.setState({ modalShow: false});
                Modal.alert('错误:' + err.response.data.detail);
            })
    }

    render() {

        const GridItem = dataItem => (
            <div style={{ padding: '12.5px' }} key={dataItem.id}>
                <img src={dataItem.avatar_url} style={{ width: '100px', height: '100px' }} alt="" />
                <div style={{ color: '#888', fontSize: '14px', marginTop: '12px' }}>
                    <p>{dataItem.id}</p><hr/>
                    <p><span>{dataItem.name}</span></p>
                    <p><span style={{color: 'blue'}}>{dataItem.org}</span></p>
                </div>
                <br />
                <div><span style={{ fontSize: '16px', color: '#FF6E27' }}>得票数：{dataItem.counter}</span></div>
            </div>
        )
        return (
            <div>

            <NavBar>医师协会视频投票系统</NavBar>
            <NoticeBar>点击单个窗口了解视频详情，每人每天能投3票,投票时间9月26日至9月30日</NoticeBar>

                <Grid
                    data={this.state.dataArray}
                    columnNum={3}
                    renderItem={GridItem}
                    onClick={this.onGridClick}
                    square={false}
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
                    <div style={{ height: '450px', overflow: 'scroll', width: '100%' }}>
                        <h2>{this.state.modalValue.id}.{this.state.modalValue.name}</h2>
                        <p>{this.state.modalValue.desc}</p>
                        <p style={{color: 'blue'}}>(点击图片观看完整视频)</p>
                        <p><a href={this.state.modalValue.info_url}><img src={this.state.modalValue.avatar_url} alt="" style={{width: '100%'}} /></a></p>
                    </div>
                </Modal>
            </div>
        );
    }
}

export default VotePage;