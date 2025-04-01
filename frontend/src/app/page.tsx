
"use client";
import { useEffect, useState } from "react";
import { Card, Col, Row, Typography, Spin, message, Layout } from "antd";
import axios from "axios";

const { Title } = Typography;
const { Header, Content, Footer } = Layout;

export default function Home() {
  const [produtos, setProdutos] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios
      .get("http://localhost:8000/products")
      .then((res) => setProdutos(res.data))
      .catch(() => message.error("Erro ao buscar produtos"))
      .finally(() => setLoading(false));
  }, []);

  return (
    <Layout style={{ minHeight: "100vh" }}>
      <Header style={{ background: "#001529" }}>
        <Title level={3} style={{ color: "white", margin: 0 }}>
          🛒 Loja Online
        </Title>
      </Header>

      <Content style={{ padding: "2rem" }}>
        <Title level={2}>Produtos Disponíveis</Title>
        {loading ? (
          <Spin size="large" />
        ) : (
          <Row gutter={[16, 16]}>
            {produtos.map((produto) => (
              <Col span={6} key={produto.id}>
                <Card
                  hoverable
                  title={produto.productName}
                  cover={
                    <img
                      alt={produto.productName}
                      src={produto.imageUrl[0]}
                      style={{ height: 200, objectFit: "cover" }}
                    />
                  }
                >
                  <p><strong>Categoria:</strong> {produto.productCategory}</p>
                  <p><strong>Preço:</strong> R$ {produto.price}</p>
                </Card>
              </Col>
            ))}
          </Row>
        )}
      </Content>

      <Footer style={{ textAlign: "center" }}>
        © {new Date().getFullYear()} Projeto Ecommerce - Big Data & Cloud
      </Footer>
    </Layout>
  );
}
