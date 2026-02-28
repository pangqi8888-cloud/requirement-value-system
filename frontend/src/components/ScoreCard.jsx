import React from 'react';
import { Card, Row, Col, Tag, Divider } from 'antd';
import {
  Radar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
} from 'recharts';

const ScoreCard = ({ requirement }) => {
  if (!requirement) return null;

  // 新版评估维度
  const radarData = [
    { subject: '普适性', score: requirement.universality_score || requirement.business_value_score, fullMark: 100 },
    { subject: '竞品对比', score: requirement.competitor_score, fullMark: 100 },
    { subject: '收益潜力', score: requirement.revenue_score || requirement.user_impact_score, fullMark: 100 },
  ];

  const getScoreColor = (score) => {
    if (score >= 80) return '#52c41a';
    if (score >= 60) return '#1890ff';
    if (score >= 40) return '#faad14';
    return '#ff4d4f';
  };

  const getPriorityTag = (score) => {
    if (score >= 80) return <Tag color="red">高优先级</Tag>;
    if (score >= 60) return <Tag color="orange">中优先级</Tag>;
    return <Tag color="default">低优先级</Tag>;
  };

  return (
    <Card
      title={
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <span>AI 评估结果</span>
          {getPriorityTag(requirement.total_score)}
        </div>
      }
      style={{ marginTop: 16 }}
    >
      <Row gutter={16}>
        <Col span={12}>
          <div style={{ textAlign: 'center', marginBottom: 16 }}>
            <div style={{ fontSize: 48, fontWeight: 'bold', color: getScoreColor(requirement.total_score) }}>
              {requirement.total_score?.toFixed(1) || '0.0'}
            </div>
            <div style={{ fontSize: 16, color: '#666' }}>综合得分</div>
          </div>

          <Divider />

          <div style={{ padding: '0 16px' }}>
            {radarData.map((item) => (
              <div key={item.subject} style={{ marginBottom: 12 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4 }}>
                  <span>{item.subject}</span>
                  <span style={{ fontWeight: 'bold', color: getScoreColor(item.score) }}>
                    {(item.score || 0).toFixed(1)}
                  </span>
                </div>
                <div style={{ height: 8, background: '#f0f0f0', borderRadius: 4, overflow: 'hidden' }}>
                  <div
                    style={{
                      height: '100%',
                      width: `${item.score || 0}%`,
                      background: getScoreColor(item.score),
                      transition: 'width 0.3s',
                    }}
                  />
                </div>
              </div>
            ))}
          </div>
        </Col>

        <Col span={12}>
          <ResponsiveContainer width="100%" height={300}>
            <RadarChart data={radarData}>
              <PolarGrid />
              <PolarAngleAxis dataKey="subject" />
              <PolarRadiusAxis angle={90} domain={[0, 100]} />
              <Radar
                name="评分"
                dataKey="score"
                stroke="#1890ff"
                fill="#1890ff"
                fillOpacity={0.6}
              />
            </RadarChart>
          </ResponsiveContainer>
        </Col>
      </Row>

      {requirement.ai_recommendation && (
        <>
          <Divider />
          <div>
            <h4>AI 评估建议</h4>
            <div style={{ whiteSpace: 'pre-wrap', lineHeight: 1.8, color: '#666' }}>
              {requirement.ai_recommendation}
            </div>
          </div>
        </>
      )}
    </Card>
  );
};

export default ScoreCard;
